from django import forms

class SignupForm(forms.Form):
    email = forms.EmailField()

    def save(self,
             subject_template_name='signup/signup_subject.txt',
             email_template_name='signup/signup_email.html',
             user=None):
        """
        Send an email to the admin about the new signup.
        """
        from django.core.mail import send_mail
        if user is not None:
	        subject = loader.render_to_string(subject_template_name, user)
	        # Email subject *must not* contain newlines
	        subject = ''.join(subject.splitlines())
	        email = loader.render_to_string(email_template_name, user)
	        send_mail(subject, email, EMAIL_HOST_USER, [EMAIL_HOST_USER], fail_silently=False)