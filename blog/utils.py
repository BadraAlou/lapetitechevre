from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

@login_required
def send_order_confirmation_email(request, subject, message, recipient_list):
    user_email = request.user.email  # Adresse email de l'utilisateur connecté
    from_email = f"La Petite Chèvre <{user_email}>"

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
