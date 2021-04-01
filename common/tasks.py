from izufang import app


@app.task
def display_info(content):
    print(content)
