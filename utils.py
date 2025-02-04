import httpx # type: ignore

EMAIL_SERVICE_URL = "http://localhost:3000/api/send-email"

async def notify_email(action: str, data: dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(EMAIL_SERVICE_URL, json={"action": action, "data": data})
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as error:
        print(f"Erro ao chamar serviço de e-mail: {error.response.status_code} - {error.response.text}")
    except Exception as error:
        print(f"Erro inesperado ao enviar e-mail: {str(error)}")
