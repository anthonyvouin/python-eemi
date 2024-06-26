
def getHtmlContent(name:str):
    return  """
    <html>
        <head>
            <title>Ma page</title>
        </head>
        <body>
           <h1>Hello <span>{}</span></h1>
        </body>
    </html>
    """.format(name)