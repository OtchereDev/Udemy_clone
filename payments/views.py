from django.core.exceptions import ValidationError
from payments.models import Payment, PaymentIntent
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from courses.models import Course
import json
from decimal import Decimal


stripe.api_key=settings.STRIPE_SECRET_KEY
endpoint_secret=settings.WEBHOOK_SECRET

class PaymentHandler(APIView):

    def post(self,request):

        if request.body:
            body=json.loads(request.body)
            if body and len(body):
                # fetch course detail as line_items
                courses_line_items=[]
                cart_course=[]
                for item in body:
                    try:
                        course=Course.objects.get(course_uuid=item)

                        line_item={
                            'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(course.price*100),
                            'product_data': {
                                'name': course.title,
                             
                            },
                        },
                            'quantity': 1,
                        }

                        courses_line_items.append(line_item)
                        cart_course.append(course)

                    except Course.DoesNotExist:
                        pass
                    except ValidationError:
                        pass

            else:
                return Response(status=400)
        else:
                return Response(status=400)
        
        
        checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=courses_line_items,
                mode='payment',
                success_url='http://localhost:3000/',
                cancel_url="http://localhost:3000/",
                
            )

        
        intent=PaymentIntent.objects.create(
            payment_intent_id=checkout_session.payment_intent,
            checkout_id=checkout_session.id,
            user=request.user,
        )

        for course in cart_course:
            intent.courses.add(course)

        
        return Response({"url":checkout_session.url})



class Webhook(APIView):

    def post(self,request,*args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return Response(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return Response(status=400)


        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            
            try:
                # fetch user intent
                intent=PaymentIntent.objects.get(
                    payment_intent_id=session.payment_intent,
                    checkout_id=session.id
                    
                )
            except PaymentIntent.DoesNotExist:
                return Response(status=400)
            
            # create payment reciept
            Payment.objects.create(
                payment_intent=intent,
                total_amount= Decimal(session.amount_total)/100,
            )

            for course in intent.courses.all():
            # TODO add course to user profile
                intent.user.paid_course.add(course)

    # Fulfill the purchase...
    # fulfill_order(session)

  # Passed signature verification
        return Response(status=200)

