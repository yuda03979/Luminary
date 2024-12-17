import sys
import readchar
import termcolor

def exiting_luminary():
     print("\nExiting Luminary...")
     sys.exit(0)


def input_with_placeholder(prefix=">>> ", placeholder="send your message "):
    print('\n\n' + prefix, end='', flush=True)
    
    input_text = []
    
    # Print the placeholder in gray
    print(termcolor.colored(placeholder, 'grey'), end='', flush=True)
    sys.stdout.write(f"\r{prefix}")
    sys.stdout.flush()

    while True:
        # Read a single character
        char = readchar.readchar()

        # Handle special keys
        if char == '\r' or char == '\n':  # Enter key
            # If no input, keep placeholder
            if not input_text:
                continue
            break
        
        elif char == '\x7f':  # Backspace
            if input_text:
                input_text.pop()
        
        elif char == '\x03':  # Ctrl+C
            raise KeyboardInterrupt
        
        else:
            input_text.append(char)

        # Clear the line
        sys.stdout.write('\r>>> ' + ' ' * 80 + '\r>>> ')
        
        # If input exists, print the current input
        if input_text:
            sys.stdout.write(''.join(input_text))
        else:
            # If no input, show placeholder again
            sys.stdout.write(termcolor.colored(placeholder, 'grey'))
        
        sys.stdout.flush()
    print('\n')
    return ''.join(input_text)
