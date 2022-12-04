import asyncio


async def extract_params(message_text):
    params = message_text.split(" ")
    options = {}
    for i in range(len(params)):
        if params[i][0] == "-":
            parameter = params[i]
            if params[i + 1][0] == '"' or params[i + 1][0] == "'":
                quote = params[i + 1][0]
                stroka = ""

                while params[i + 1][::-1][0] != quote:
                    stroka += f" {params[i + 1]}"
                    i = i + 1
                stroka += f" {params[i + 1]}"

                options.update({parameter: stroka[2:len(stroka) - 1]})
            else:
                options.update({parameter: params[i + 1]})
    return options
