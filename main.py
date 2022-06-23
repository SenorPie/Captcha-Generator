import random, string, datetime, json
from PIL import Image, ImageDraw, ImageFilter, ImageFont


class CaptchaGenerator:
    """
        A class used to generate and validate captchas.

        Methods
        -------
        generate_captcha(export_path: str="")
            Generates a new captcha using pillow and adds on the important filters
        
        generate_string() -> str
            Returns a randomly 5 letter string in all caps

        get_random_color() -> tuple
            Returns a tuple with 3 randomly generated values ranging from 0-255
        
        export_captcha(img_path, captcha_code)
            A function that appends to a JSON file with the path to the captcha image and correct answer
        ------
    """

    def generate_captcha(self, export_path: str=""):
        """
            Generates the random captcha using PILLOW and our other functions created.

            Parameters
            ----------
            export_path: str, defaults to empty quotes.
        """

        # Captcha text
        captcha_text = self.generate_string()
        
        # Create our image
        new_img = Image.new(mode='RGB', size=(100, 100), color=((255, 255, 255)))
        
        # Start drawing text
        draw = ImageDraw.Draw(new_img)

        # Create a for loop for the amount of letters there are in our captcha text
        for i in range(len(captcha_text)):
            # Set our font and font-size being random
            font = ImageFont.truetype("arial.ttf", random.randrange(20, 26))

            # Set the X position to X=25 + whatever iteration we are on times 12, y is between 30-50
            xy_pos = (25+i*12, random.randrange(30, 50))

            # Draw our letter on the xy position above and fill it in with a random color
            draw.text(xy_pos, captcha_text[i], fill=self.get_random_color(), font=font)


        # Draw 8 lines in random positions throughout the image
        for i in range(8):
            draw.line((random.randrange(0, 100), random.randrange(0, 100)) + (random.randrange(0, 100), random.randrange(0, 100)), fill=128)
        

        # Add filter
        new_img = new_img.filter(ImageFilter.MinFilter(3))

        # Get date
        date = datetime.datetime.now()

        # Save image
        img_name = f"{export_path}captcha-{date.timestamp()}.png"
        new_img.save(img_name)

        # Export to json file
        self.export_captcha(img_name, captcha_text)

        # Return the image name and correct captcha_code
        return img_name, captcha_text

    @staticmethod
    def generate_string() -> str:
        # Return a string with 5 random uppercase letters
        return "".join(random.choices(string.ascii_uppercase, k=5))

    @staticmethod
    def get_random_color() -> tuple:
        # Return a tuple with 3 random values ranging from 0-255
        return (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    
    @staticmethod
    def export_captcha(img_path: str, captcha_code: str):
        """
            Exports the captcha to a JSON file.

            Parameters
            ----------
            img_path: str, non optional
            captcha_code: str, non optional
        """

        # Filename to where we save our captchas
        filename = "captchas.json"

        # Our captcha JSON object
        captcha_obj = []

        # Open the JSON file and load the JSON data
        with open(filename) as f:
            captcha_obj = json.load(f)
        
        # Append our new object
        captcha_obj.append({
            "img_path": img_path,
            "captcha_code": captcha_code
        })

        # Write the new captcha JSON object to the file
        with open(filename, mode="w") as json_file:
                json.dump(captcha_obj, json_file, 
                          indent=4,  
                          separators=(',',': '))
    


if __name__ == "__main__":
    CaptchaGenerator().generate_captcha()
