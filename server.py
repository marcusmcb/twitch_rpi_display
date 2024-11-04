import pygame
from flask import Flask, request

app = Flask(__name__)

@app.route('/display_lotto', methods=['POST'])
def display_message():
    message = request.json.get('message', 'Hello, Twitch!')
    print("MESSAGE: ", message)    
    display_text(message)
    return "Message displayed", 200  

@app.route('/display_fortune', methods=['POST'])
def display_fortune():
    message = request.json.get('message', 'Your fortune awaits!')
    print("FORTUNE MESSAGE: ", message)
    # For now, we’re just printing the message.
    # You can add a display_text(message) or similar functionality later as needed.
    return "Fortune message received", 200

def display_text(text):
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Fullscreen mode
    pygame.display.set_caption('Message Display')
    screen_width, screen_height = screen.get_width(), screen.get_height()

    # Split the message into parts based on the format
    # Expected format: "<username> lucky numbers: <numbers>"
    try:
        username_part, numbers_part = text.split(" lucky numbers: ")
        line1 = username_part
        line2 = "lucky numbers:"
        line3 = numbers_part
    except ValueError:
        # Fallback if the message format is different
        line1 = text
        line2 = ""
        line3 = ""

    # Store lines in an array
    lines = [line1, line2, line3]

    # Set margins and calculate the maximum font size to fit within the screen
    margin = 20  # Margin from the screen borders in pixels
    max_text_width = screen_width - 2 * margin
    max_text_height = screen_height - 2 * margin
    font_size = 100  # Start with a large font size

    # Load the custom font (replace 'Roboto-Regular.ttf' with the actual font path if needed)
    font_path = 'fonts/Rubik-Regular.ttf'
    font = pygame.font.Font(font_path, font_size)
    
    # Adjust font size to fit the lines within the screen height
    while True:
        # Check if text width and total height fit within the screen with current font size
        text_surfaces = [font.render(line, True, (255, 243, 0)) for line in lines if line]
        text_heights = sum(surface.get_height() for surface in text_surfaces) + font.get_height()  # Add extra space for empty line
        if all(surface.get_width() <= max_text_width for surface in text_surfaces) and text_heights <= max_text_height:
            break
        # Reduce font size if text doesn't fit
        font_size -= 1
        font = pygame.font.Font(font_path, font_size)

    # Set background color and position lines vertically centered with equal spacing
    screen.fill((78, 48, 184))
    y_offset = (screen_height - text_heights) // 2
    for i, surface in enumerate(text_surfaces):
        screen.blit(surface, ((screen_width - surface.get_width()) // 2, y_offset))
        y_offset += surface.get_height()
        # Add extra space after line 2 to create an empty line
        if i == 1:  # This is after rendering line2
            y_offset += font.get_height() // 2  # Adjust this as needed for more or less space

    # Update display
    pygame.display.flip()

    # Keep the display for a set duration
    pygame.time.delay(30000)  # Display message for 5 seconds
    pygame.quit()  # Clear the screen after



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
