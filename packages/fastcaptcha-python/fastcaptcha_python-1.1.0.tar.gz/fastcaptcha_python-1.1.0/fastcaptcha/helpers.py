import base64


def convert_img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())
        return b64_string.decode("utf8")
