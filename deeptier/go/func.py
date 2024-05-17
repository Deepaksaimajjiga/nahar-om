from .models import *
from .utility import SendEmail



try:
        link = "__123__"
        email = "vickytilotia12344@gmail.com"
        purpose = "Refferal"
        SendEmail(
            link=link,
            email=email(),
            purpose=purpose,
        #     attachment_path=model_instance.file.path,
         )
except Exception as e:
        print(f"Error Sending to buyer {e}")