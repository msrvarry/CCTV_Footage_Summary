import os
import google.generativeai as genai

# Configure the Google Generative AI API with your API key
API_KEY = os.environ.get("GOOGLE_API_KEY", "insert api key")  # Replace with your API key or set environment variable
genai.configure(api_key=API_KEY)

def upload_video(file_path):
    """
    Uploads a video file to the Gemini API and returns the file object.
    Args:
        file_path (str): Path to the local video file.
    Returns:
        Uploaded file object.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Video file {file_path} not found.")
        print(f"Uploading video: {file_path}")
        video_file = genai.upload_file(path=file_path, mime_type="video/mp4")
        print(f"Uploaded video: {video_file.uri}")
        return video_file
    except Exception as e:
        print(f"Error uploading video: {e}")
        raise

def generate_summary(video_file, model_name="models/gemini-1.5-flash"):
    """
    Generates a summary of the video using the Gemini 1.5 Flash model.
    Args:
        video_file: The uploaded video file object.
        model_name (str): The Gemini model to use (default: gemini-1.5-flash).
    Returns:
        str: The generated summary text.
    """
    try:
        model = genai.GenerativeModel(model_name)
        prompt = """
        Analyze the provided CCTV footage and generate a concise summary of the events occurring in the video.
        Focus on key activities, movements, or notable occurrences. Do not make assumptions beyond what is visible.
        Provide the summary in a clear, chronological order, and limit it to 3-5 sentences.
        """
        print("Generating summary...")
        response = model.generate_content([prompt, video_file])
        summary = response.text.strip()
        print("Summary generated successfully.")
        return summary
    except Exception as e:
        print(f"Error generating summary: {e}")
        raise

def save_summary(summary, output_file="summary.txt"):
    """
    Saves the summary to a text file.
    Args:
        summary (str): The summary text to save.
        output_file (str): The path to the output text file (default: summary.txt).
    """
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"Summary saved to {output_file}")
    except Exception as e:
        print(f"Error saving summary: {e}")
        raise

def main(video_path):
    """
    Main function to process the video and generate a summary.
    Args:
        video_path (str): Path to the input video file.
    """
    try:
        # Upload the video
        video_file = upload_video(video_path)
        
        # Generate the summary
        summary = generate_summary(video_file)
        
        # Save the summary to a file
        save_summary(summary)
        
        # Delete the uploaded file from Gemini API
        genai.delete_file(video_file.name)
        print(f"Deleted uploaded video: {video_file.name}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Specify the path to your video file
    VIDEO_PATH = r"sample_video2.mp4"  # Update with your video file path
    main(VIDEO_PATH)