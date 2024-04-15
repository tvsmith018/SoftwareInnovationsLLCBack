from adrf.views import APIView
from django.http import JsonResponse

import multiprocessing
from django.template.loader import get_template
from django.core.mail import EmailMessage

from .models import inquires


class InquireProcessing:
    firstname: str
    lastname: str
    email: str
    phone: str
    message: str

    def processingData(self, data, return_dic):
        self.firstname = data['firstname']
        self.lastname = data['lastname']
        self.email = data['email']
        self.phone = data['phone']
        self.message = data['message']

        self.firstname = self.firstname.upper()
        self.lastname = self.lastname.upper()
        self.email = self.email.lower()

        if self.message is not None:
            self.message = self.message.upper()
        try:
            if (self.message is not None):
                newInquire = inquires(firstname=self.firstname, lastname=self.lastname, email=self.email, phone=self.phone, message=self.message)
            else:
                newInquire = inquires(firstname=self.firstname, lastname=self.lastname, email=self.email, phone=self.phone, message='')
            newInquire.save()
            return_dic['inquirymessage'] = 'inquiry saved'
        except Exception:
            return_dic['inquirymessage'] = 'inquiry not able to be saved'


class EmailProcess:

    def sendingEmail(self, data, return_dic):
        fistname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        subject = 'Thank you for inquiring'
        messageData = {
            'firstname': fistname.capitalize(),
            'lastname': lastname.capitalize(),
        }

        try:
            message = get_template('email_templates/inquiry.html').render(messageData)
            msg = EmailMessage(
                subject,
                message,
                '',
                [email.lower()],
            )
            msg.content_subtype = "html"
            msg.send()
            return_dic['emailmessage'] = 'email successfully sent'
        except Exception:
            return_dic['emailmessage'] = 'email failed to send'


class InquiryAPI(APIView):
    processor = InquireProcessing()
    emailprocess = EmailProcess()

    async def post(self, request):
        data = request.data
        context = {}
        process1manager = multiprocessing.Manager()
        process2manager = multiprocessing.Manager()
        process1returndic = process1manager.dict()
        process2returndic = process2manager.dict()
        process1 = multiprocessing.Process(target=self.processor.processingData, args=(data, process1returndic))
        process2 = multiprocessing.Process(target=self.emailprocess.sendingEmail, args=(data, process2returndic))
        process1.start()
        process2.start()
        process1.join()
        process2.join()
        if process1returndic['inquirymessage'] == 'inquiry saved' and process2returndic['emailmessage'] == 'email successfully sent':
            context['message'] = 'processes successfully completed'
        if process1returndic['inquirymessage'] == 'inquiry not able to be saved' or process2returndic['emailmessage'] == 'email failed to send':
            context['message'] = 'one or more processess failed to complete'
        return JsonResponse(context)
