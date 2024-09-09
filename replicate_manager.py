import replicate # type: ignore
import asyncio
from config import REPLICATE_API_TOKEN

class ReplicateManager:
    def __init__(self):
        self.client = replicate.Client(api_token=REPLICATE_API_TOKEN)
        self.model = "cjwbw/sadtalker"
        self.version = "a519cc0cfebaaeade068b23899165a11ec76aaa1d2b313d40d214f204ec957a3"
        
        
        # Default values for sadtalker adjustable parameters
        self.expression_scale = 1.0
        self.pose_style = 0
        
        # Default values for sadtalker other parameters
        self.facerender = "facevid2vid"
        self.preprocess = "crop"
        self.still_mode = False
        self.use_enhancer = False
        self.use_eyeblink = True
        self.size_of_image = 256
        self.pose_style = 38
        self.expression_scale = 1.2
        
        # video-retalker init
        self.video_retalking_model = "chenxwh/video-retalking"
        self.video_retalking_version = "db5a650c807b007dc5f9e5abe27c53e1b62880d1f94d218d27ce7fa802711d67"

      
    async def generate_video_retalking(self, face_path, audio_path):
        try:
            # Create prediction
            prediction = self.client.predictions.create(
                version=self.video_retalking_version,
                input={
                    "face": open(face_path, "rb"),
                    "input_audio": open(audio_path, "rb")
                }
            )

            # Wait for the prediction to complete asynchronously
            while prediction.status != "succeeded":
                await asyncio.sleep(5)
                prediction.reload()

            return prediction.output

        except Exception as e:
            print(f"Error in generate_video_retalking: {str(e)}")
            return None
    
        

    async def generate_talking_face(
        self,
        driven_audio,
        source_image,
        facerender=None,
        pose_style=None,
        preprocess=None,
        still_mode=None,
        use_enhancer=None,
        use_eyeblink=None,
        size_of_image=None,
        expression_scale=None
    ):
        try:
            # Use instance variables if no value is provided
            facerender = facerender if facerender is not None else self.facerender
            pose_style = pose_style if pose_style is not None else self.pose_style
            preprocess = preprocess if preprocess is not None else self.preprocess
            still_mode = still_mode if still_mode is not None else self.still_mode
            use_enhancer = use_enhancer if use_enhancer is not None else self.use_enhancer
            use_eyeblink = use_eyeblink if use_eyeblink is not None else self.use_eyeblink
            size_of_image = size_of_image if size_of_image is not None else self.size_of_image
            expression_scale = expression_scale if expression_scale is not None else self.expression_scale

            print(f"Debug - Initiating API call with parameters:")
            print(f"  driven_audio: {driven_audio}")
            print(f"  source_image: {source_image}")
            print(f"  facerender: {facerender}")
            print(f"  pose_style: {pose_style}")
            print(f"  preprocess: {preprocess}")
            print(f"  still_mode: {still_mode}")
            print(f"  use_enhancer: {use_enhancer}")
            print(f"  use_eyeblink: {use_eyeblink}")
            print(f"  size_of_image: {size_of_image}")
            print(f"  expression_scale: {expression_scale}")

            # Create a prediction using the client
            prediction = self.client.predictions.create(
                version=self.version,
                input={
                    "driven_audio": driven_audio,
                    "source_image": source_image,
                    "facerender": facerender,
                    "pose_style": pose_style,
                    "preprocess": preprocess,
                    "still_mode": still_mode,
                    "use_enhancer": use_enhancer,
                    "use_eyeblink": use_eyeblink,
                    "size_of_image": size_of_image,
                    "expression_scale": expression_scale
                }
            )

            print(f"Debug - Prediction created. ID: {prediction.id}")

            while prediction.status != "succeeded":
                print(f"Debug - Current prediction status: {prediction.status}")
                if prediction.status == "failed":
                    print(f"Debug - Prediction failed. Error: {prediction.error}")
                    return None
                await asyncio.sleep(5)  # Wait for 5 seconds before checking again
                prediction.reload()  # Refresh the prediction object

            print(f"Debug - Prediction completed. Status: {prediction.status}")
            print(f"Debug - Raw prediction output: {prediction.output}")

            # Return the output directly
            return prediction.output

        except replicate.exceptions.ModelError as e:
            print(f"Error: Model execution failed. Details: {str(e)}")
        except replicate.exceptions.ReplicateError as e:
            print(f"Error: Replicate API error occurred. Details: {str(e)}")
        except Exception as e:
            print(f"Error in generate_talking_face: {str(e)}")
            print(f"Error type: {type(e)}")
            print(f"Error args: {e.args}")
        
        return None

    def set_expression_scale(self, value):
        try:
            self.expression_scale = float(value)
            return f"Expression scale set to {self.expression_scale}"
        except ValueError:
            return "Invalid value. Please provide a number for expression scale."

    def set_pose_style(self, value):
        try:
            self.pose_style = int(value)
            return f"Pose style set to {self.pose_style}"
        except ValueError:
            return "Invalid value. Please provide an integer for pose style."

    def set_facerender(self, value):
        if value in ["facevid2vid", "pirender"]:
            self.facerender = value
            return f"Facerender set to {self.facerender}"
        else:
            return "Invalid value. Facerender must be 'facevid2vid' or 'pirender'."

    def set_preprocess(self, value):
        if value in ["full", "crop"]:
            self.preprocess = value
            return f"Preprocess set to {self.preprocess}"
        else:
            return "Invalid value. Preprocess must be 'full' or 'crop'."

    def set_still_mode(self, value):
        if value.lower() in ['true', 'false']:
            self.still_mode = value.lower() == 'true'
            return f"Still mode set to {self.still_mode}"
        else:
            return "Invalid value. Still mode must be 'true' or 'false'."

    def set_use_enhancer(self, value):
        if value.lower() in ['true', 'false']:
            self.use_enhancer = value.lower() == 'true'
            return f"Use enhancer set to {self.use_enhancer}"
        else:
            return "Invalid value. Use enhancer must be 'true' or 'false'."

    def set_use_eyeblink(self, value):
        if value.lower() in ['true', 'false']:
            self.use_eyeblink = value.lower() == 'true'
            return f"Use eyeblink set to {self.use_eyeblink}"
        else:
            return "Invalid value. Use eyeblink must be 'true' or 'false'."

    def set_size_of_image(self, value):
        try:
            self.size_of_image = int(value)
            return f"Size of image set to {self.size_of_image}"
        except ValueError:
            return "Invalid value. Please provide an integer for size of image."

    async def get_model_info(self):
        try:
            model = self.client.models.get(self.model)
            version = model.versions.get(self.version)
            return {
                "name": model.name,
                "description": model.description,
                "version": version.id
            }
        except Exception as e:
            print(f"Error in get_model_info: {str(e)}")
            return None