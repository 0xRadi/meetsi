from django.conf import settings    # import your jitsi conigrations from settings
import jwt


# user is to assign the user's details to jitsi meeting
# mod is for wether the user is a moderator or not

# the following plugin is being used to activate moderators and manage access control table
# https://github.com/0xRadi/jitsi-token-moderation-plugin  - forked from @nvonahsen

def generate(room, user=None, mod=False):
    payload = {
        "iss": settings.JWT_ISS,
        "sub": settings.JWT_SUB,
        "aud": settings.JWT_AUD,
        "room": room,
        "moderator": mod,
    }
    if user is not None:
        payload["context"] = {
            "user": {
                "id": user.username,
                "name": "{} {}".format(user.first_name, user.last_name),
            }
        }
    return jwt.encode(payload, settings.JWT_SECRET).decode('utf-8')
