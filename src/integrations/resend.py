
import resend



def send_email(email,ai_plan,city):
    resend.api_key = "xxxxxxxxxxxxxxxxxxxxxxx"
    r = resend.Emails.send({
    "from": "onboarding@resend.dev",
    "to": email,
    "subject": f"Your plan to {city} is ready!",
    "html": f"<p>Hey {email.split('@')[0]}! <br><br> Here's Your AI Travel Plan </p> <br> <p>{ai_plan}</p>"
    })


