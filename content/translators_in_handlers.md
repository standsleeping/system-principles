---
id: TRANSLATORS_IN_HANDLERS
title: "Use translators in request handlers."
essence: "Handlers receive domain commands, never raw requests, so they stay framework-independent."
---

Translate incoming requests to domain commands before passing to handlers.

```python
async def handle_request[TCommand](
    request: Request,
    translator: callable[[Request], tuple[TranslatorError | None, TCommand | None]],
    handler: CommandHandler[TCommand]
) -> Response:
    err, command = await translator(request)
    if err:
        return Response({"error": err.message}, status=400)

    result = await handler.handle(command)
    return Response({"result": result}, status=200)
```