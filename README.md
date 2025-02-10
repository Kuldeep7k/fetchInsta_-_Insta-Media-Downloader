# Instagram Media Downloader

This Flask application allows users to download media (images and videos) from Instagram posts, reels, TV, and stories by providing a valid Instagram URL.

## Features

-   Downloads images and videos from Instagram posts.
-   Supports posts, reels, TV, and stories.
-   Provides a preview of the media before downloading.
-   Handles errors and displays user-friendly messages.

## Prerequisites

-   Python 3.6+
-   Flask
-   Instaloader

## Installation

1.  Clone the repository:

    ```bash
    git clone [repository_url]
    cd [repository_directory]
    ```

2.  Install the required Python packages:

    ```bash
    pip install Flask instaloader
    ```

## Usage

1.  Run the Flask application:

    ```bash
    python app.py
    ```

2.  Open your web browser and go to `http://127.0.0.1:5000`.

3.  Enter the Instagram URL in the input field and click "Fetch Media".

4.  Preview the media and download the desired files.

## Directory Structure

-   `app.py`: Main Flask application file.
-   `templates/`: Contains HTML templates.
    -   `index.html`: Home page with the input form.
    -   `instagram_preview.html`: Page to display the fetched media.
-   `downloads/`: Directory where downloaded media is stored. The structure is `downloads/session_id/profile_name/post_shortcode/`.
-   `static/`: Contains static assets such as CSS or JavaScript files (currently not in use).

## Error Handling

The application handles the following errors:

-   Invalid URL format.
-   Instagram post not found.
-   Other exceptions during the download process.

Error messages are displayed to the user via Flask's `flash` functionality.

## Notes

-   This application uses `instaloader` to fetch Instagram data. Ensure that you comply with Instagram's terms of service when using this application.
-   The downloaded files are stored in the `downloads` directory, organized by session ID, profile name, and post shortcode.
-   The session ID is stored in a cookie to manage downloads.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests.

## License

[License](https://github.com/Kuldeep7k/fetchInsta_-_Insta-Media-Downloader/blob/main/LICENSE)
