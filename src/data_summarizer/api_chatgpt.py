from openai import OpenAI


def chatgpt_call(text: str, company_name: str) -> str:
    api_key = "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"
    client = OpenAI(api_key=api_key)

    message_content = (
        f"""me haces un resumen de este html de la empresa {company_name}, 
                    en un maximo de 3 lineas que resuma a que se dedica dicha empresa por favor.
                      Respira profundamente y trabajo en este problema paso a paso:"""
        + text
    )
    # Enviar solicitud de completación de chat
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0301",
        messages=[{"role": "user", "content": message_content}],
        stream=False,
    )

    choices = response.choices
    if choices:
        first_choice = choices[0]
        message = first_choice.message
        content = message.content
        if manage_name_company_errors(content):
            return "COMPANY_NAME and URL not exact"
        return content
    else:
        return None


def manage_name_company_errors(text: str) -> bool:
    if str(text).lower().find("html") != -1:
        return True

    return False
