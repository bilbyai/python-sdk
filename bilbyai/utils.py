from google.cloud import documentai_v1beta3 as documentai
from google.cloud import translate_v2 as translate


def documentai_process_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
) -> documentai.Document:
    """Takes a file and returns a Document object containing the extracted text.

    Args:
        `project_id` (str): The ID of the Google Cloud project you want to use, like `bilbyai-dev`.
        `location` (str): The location of the Google Cloud project you want to use, like `us`.
        `processor_id` (str): The ID of the Document AI processor you want to use, like `2370ba2d4e3b3c3e`.
        `file_path` (str): The path to the file you want to analyze, like `path/to/file.pdf`.
        `mime_type` (str): The MIME type of the file you want to analyze, like `application/pdf`.
            Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types.

    Returns:
        documentai.Document: The Document object containing the extracted text.
    """

    # Define an options dictionary, which includes the API's URL. This is used to connect to Google's Document AI service
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}

    # Create a Document AI client, think of it as our bridge for communicating with Google's services
    documentai_client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # Generate the complete name of the processor
    # You need to first create a processor in the Google Cloud console
    resource_name = documentai_client.processor_path(project_id, location, processor_id)

    # Read in the document you want to analyze (like an image or PDF), and store it in the variable image_content
    with open(file_path, "rb") as image:
        image_content = image.read()

        # Convert the read document into a format that Google Document AI can understand, i.e., a RawDocument object
        raw_document = documentai.RawDocument(
            content=image_content, mime_type=mime_type
        )
        # Create a request, which includes the name of the processor and the document we want to analyze
        request = documentai.ProcessRequest(
            name=resource_name, raw_document=raw_document
        )
        # Send our request and receive the analysis results
        result = documentai_client.process_document(request=request)

        # Return this analysis result
        return result.document


def pdf_extract_text(file_path: str) -> str:
    """Given a PDF file, extract the text from it using Google Document AI.

    Usage: `pdf_extract_text("path/to/file.pdf")`

    Args:
        `file_path` (str): The path to the PDF file.

    Returns:
        `str`: The text extracted from the PDF file.
    """
    return documentai_process_document(
        project_id="bilbyai-dev",
        location="us",
        processor_id="2370ba2d4e3b3c3e",
        file_path=file_path,
        mime_type="application/pdf",
    ).text


def google_translate_text(text: str, target_language: str) -> str:
    """Given a text, translate it to the target language using Google Translate.

    Usage: `translate_text("Hello world", "zh-CN")`

    Args:
        `text` (str): The text to translate.
        `target_language` (str): The target language to translate to, like `zh-CN`.

    Returns:
        `str`: The translated text.
    """
    # Create a Google Translate client, think of it as our bridge for communicating with Google's services
    translate_client = translate.Client()

    # Translate the text to the target language
    result = translate_client.translate(text, target_language=target_language)

    # Return the translated text
    return result["translatedText"]
