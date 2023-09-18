## Development Task for AI Piping

Backend, Python + FastAPI 

**Objective:** Create a simple FastAPI application that serves an endpoint to recommend three things to do in a given country during a specific season by consulting the OpenAI API.

### Instructions:

1. **Setup**:
   - Initialize a new Python project.
   - Install FastAPI and any other required libraries.

2. **API Endpoint**:
   - Design an endpoint with a custom route for travel recomendations.
   - This endpoint should accept two query parameters:
     - `country`: The country for which the recommendations are to be fetched.
     - `season`: The season in which the recommendations are desired (e.g., "summer", "winter").

     Both parameters are required. The season must validate that one of the 4 seasons are choosen.
   
   - Use localhost:3000 

   - No auth required for the endpoint/API
   - No encryption, no https... Keep it simple

3. **OpenAI GPT Integration**:
   - Call the OpenAI GPT API with a crafted prompt based on the given `country` and `season`.
   - You will need to craft the API prompt yourself.
   - Parse the response to extract the recommendations.
   - You can use the OpenAI python library or directly call the endpoint.
   - To make API calls to OpenAI, you'll need an API key. Ask for it to Urbano.

4. **Response**:
   - The endpoint should return a JSON response with the recommendations. An example format is:
     ```json
     {
       "country": "Canada",
       "season": "winter",
       "recommendations": [
         "Go skiing in Whistler.",
         "Experience the Northern Lights in Yukon.",
         "Visit the Quebec Winter Carnival."
       ]
     }
     ```

5. **Additional (Optional, not required)**:
   - You could use Docker to containerize the application.
   - You could write tests for the application to ensure it behaves as expected.
   - If you consider yourself full stack, and want to showcase your skills, you can create a simple frontend that calls this API 

6. **Submission**:
   - Push your code to a public GitHub repository.
   - Include a `README.md` with clear instructions on how to run the application, test it, and any other relevant information.

### Evaluation Criteria:

1. **Functionality**: Does the application work as described?
2. **Code Quality**: Is the code organized, clean, and free of bugs?
3. **API Design**: Is the API intuitive and easy to understand?
4. **Integration**: Is the OpenAI GPT API integrated seamlessly, and are errors handled gracefully?
5. **Documentation**: Are the setup and usage instructions clear?

### Documentation:

- FastAPI documentation: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- OpenAI GPT API documentation: [https://platform.openai.com/docs/api-reference](https://platform.openai.com/docs/api-reference)

