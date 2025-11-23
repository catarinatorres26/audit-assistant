from mangum import Mangum
from app.api import app

# Este é o handler que a AWS Lambda vai chamar
handler = Mangum(app)
