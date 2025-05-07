from together import AsyncTogether,Together
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
together_api_key = os.getenv("TOGETHER_API_KEY")

client = Together()
async_client = AsyncTogether() 

user_prompt = input("Ask : ")

reference_models = [
    "Qwen/Qwen2-72B-Instruct",
    "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    "mistralai/Mixtral-8x22B-Instruct-v0.1"
]
aggregator_model = "mistralai/Mixtral-8x22B-Instruct-v0.1"
aggreagator_system_prompt = """
                            You have been provided with a set of responses from various open-source models to the latest user query. 
                            Your task is to synthesize these responses into a single, high-quality response. 
                            It is crucial to critically evaluate the information provided in these responses, recognizing that some of it may be biased or incorrect. 
                            Your response should not simply replicate the given answers but should offer a refined, accurate, and comprehensive reply to the instruction. 
                            Ensure your response is well-structured, coherent, and adheres to the highest standards of accuracy and reliability.
                            """
                            
async def run_llm(model):
    response = await async_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": user_prompt}],
        max_tokens=1024,
        temperature=0.1,
    )
    print(model)
    return response.choices[0].message.content 

async def main():
    try:
        results = await asyncio.gather(*[run_llm(model) for model in reference_models])
        final_response = ""
        try:
            for chunk in client.chat.completions.create(
                model=aggregator_model,
                messages=[
                    {"role": "system", "content": aggreagator_system_prompt},
                    {"role": "user", "content": ",".join(str(element) for element in results)},
                ],
                stream=True,
            ):
                try:
                    if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                        final_response += chunk.choices[0].delta.content
                        print(chunk.choices[0].delta.content, end="", flush=True)
                except (IndexError, AttributeError) as e:
                    continue
        except Exception as e:
            print(f"\nError during streaming: {str(e)}")
        return final_response
    except Exception as e:
        print(f"\nError during execution: {str(e)}")
    finally:
        # Remove the close() call since AsyncTogether doesn't support it
        pass

if __name__ == "__main__":
    asyncio.run(main())


