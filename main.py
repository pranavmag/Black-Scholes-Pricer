from fastapi import FastAPI
from pydantic import BaseModel
from pricer import BlackScholesPricer

app = FastAPI(title="Black-Scholes Pricing API")

class OptionInput(BaseModel):
    current_asset_price: float
    strike_price: float
    time_to_expiration: float
    risk_free_interest_rate: float
    volatility: float

@app.post("/calculate-options")
def calculate_options(data: OptionInput):
    pricer = BlackScholesPricer(
        current_asset_price=data.current_asset_price,
        strike_price=data.strike_price,
        time_to_expiration=data.time_to_expiration,
        risk_free_interest_rate=data.risk_free_interest_rate,
        volatility=data.volatility
    )

    call = pricer.calculate_call_price()
    put = pricer.calculate_put_price()

    return {
        "call_price": round(call, 2),
        "put_price": round(put, 2),
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)