from dotenv import load_dotenv
import minio
from minio.error import S3Error
import io
import os


class ImageRepository:

    def __init__(self):

        load_dotenv("garage/.env.garage")

        access_key=os.getenv("GARAGE_DEFAULT_ACCESS_KEY")
        secret_key=os.getenv("GARAGE_DEFAULT_SECRET_KEY")

        print(f"Access: {access_key}")
        print(f"Secret: {secret_key}")

        self.client = minio.Minio(
            "192.168.56.253:3900",
            access_key,
            secret_key,
            region="garage",
            secure=False,
        )

    def getImageByURL(self, url_path):

        byte_image=None
        image_type=None

        try:
            response=self.client.get_object("photo-bucket", url_path)
            byte_image=response.read()
            image_type=response.headers["content-type"].split("/")[1]

        except S3Error as e:
            print(f"ERROR: {e.message}")
        finally:
            response.close()

        return byte_image, image_type

    def putImageByURL(self, byte_image, image_type, url_path):

        response = self.client.put_object(
            "photo-bucket",
            url_path,
            io.BytesIO(byte_image),
            len(byte_image),
            f"image/{image_type}"
        )

        return response
            

