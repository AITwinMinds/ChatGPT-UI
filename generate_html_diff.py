import difflib
import html

def show_diff_light(seqm):
    output = []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(html.escape(seqm.a[a0:a1]))
        elif opcode == 'insert':
            output.append(
                f"<ins style='color: green; font-weight: bold;'>{html.escape(seqm.b[b0:b1])}</ins>")
        elif opcode == 'delete':
            output.append(
                f"<del style='color: red; font-weight: bold;'>{html.escape(seqm.a[a0:a1])}</del>")
        elif opcode == 'replace':
            output.append(
                f"<del style='color: red; font-weight: bold;'>{html.escape(seqm.a[a0:a1])}</del><ins style='color: green; font-weight: bold;'>{html.escape(seqm.b[b0:b1])}</ins>")
        else:
            raise RuntimeError(f"Unexpected opcode: {opcode}")

    return ''.join(output)

def show_diff_dark(seqm):
    output = []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(html.escape(seqm.a[a0:a1]))
        elif opcode == 'insert':
            output.append(
                f"<ins style='color: #6ee183; font-weight: bold;'>{html.escape(seqm.b[b0:b1])}</ins>")
        elif opcode == 'delete':
            output.append(
                f"<del style='color: #fb3f4b; font-weight: bold;'>{html.escape(seqm.a[a0:a1])}</del>")
        elif opcode == 'replace':
            output.append(
                f"<del style='color: #fb3f4b; font-weight: bold;'>{html.escape(seqm.a[a0:a1])}</del><ins style='color: #6ee183; font-weight: bold;'>{html.escape(seqm.b[b0:b1])}</ins>")
        else:
            raise RuntimeError(f"Unexpected opcode: {opcode}")

    return ''.join(output)


def generate_html_diff(original_text, corrected_text, dark_mode=False):
    bg_color = "#222529" if dark_mode else "#f8f8f8"
    text_color = "#ffffff" if dark_mode else "#000000"
    ins_color = "#1c3921" if dark_mode else "#e6ffed"
    del_color = "#3a171a" if dark_mode else "#ffe6e6"

    sm = difflib.SequenceMatcher(None, original_text, corrected_text)
    if dark_mode:
        diff_html = show_diff_dark(sm)
    else:
        diff_html = show_diff_light(sm)

    # Customize the HTML structure and add styles
    html_output = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: {bg_color};
                    color: {text_color};
                }}
                ins {{
                    background-color: {ins_color};
                }}
                del {{
                    background-color: {del_color};
                }}
                .version {{
                    margin-bottom: 20px;
                }}
                .header {{
                    font-size: larger;
                    font-weight: bold;
                }}
                .highlighted-text {{
                    font-size: larger;
                }}
            </style>
        </head>
        <body>
            <div class="version">
                <div class="header">Original Text:</div>
                <div class="highlighted-text">{html.escape(original_text)}<br></div>
            </div>
            <div class="version">
                <div class="header">Differences Highlighted:</div>
                <div class="highlighted-text">{diff_html}<br></div>
            </div>
            <div class="version">
                <div class="header">Corrected Text:</div>
                <div class="highlighted-text">{html.escape(corrected_text)}</div>
            </div>
        </body>
    </html>
    """

    return html_output


