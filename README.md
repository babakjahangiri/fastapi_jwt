# FastAPI JWT
FastAPI authentication system using JWT and OAuth2, leveraging libraries like Passlib's bcrypt and Python-JOSE for enhanced security. It serves as a hands-on practice to integrate modern authentication techniques within a FastAPI application.



### Payload

In a JWT (JSON Web Token) payload, you typically store information that needs to be communicated between parties in a secure and verifiable manner. This can include:


- **User Identification**: Storing the user's ID or username to identify them.
- **Expiration Time**: Setting an expiration time to limit the token's validity.
- **Issued At**: Storing the timestamp when the token was issued.
- **Issuer**: Indicating who issued the token (e.g., your server's domain).
- **Subject**: Identifying the subject of the token (usually the user).
- **Custom Claims**: Any additional information relevant to your application.

💡 Avoid storing sensitive data like passwords or confidential information. Instead, use the payload to store a unique identifier and perform server-side checks when needed.

📝  Remember that while the payload can be decoded by anyone who has the token, the information within is digitally signed by the issuing party to ensure its integrity and authenticity. Always validate tokens before trusting their content.


### Database Schema

Create a table (or a collection if you're using a NoSQL database) to store tokens. The schema could look something like this:

**token_id**: A unique identifier for the token.(in MongoDB is _id)
**user_id**: The identifier for the user to whom the token was issued.
**jwt_token**: The actual JWT token string.
💡 _Whenever you issue a new JWT, save its details in the database. You may not necessarily need to store the whole token if you can identify tokens uniquely through other means (like using a jti claim in the JWT)._


**issued_at** : Timestamp when the token was issued.
**expires_at** : Timestamp when the token will expire.
**revoked**: A boolean flag indicating if the token has been revoked.
**jti**: generate a unique value for the jti claim. This could be a random string, a UUID, or any other unique value



#### Overview of the jti claim:

The jti claim in a JWT (JSON Web Token) stands for "JWT ID". It's a unique identifier for the token and can be used to prevent the JWT from being replayed, essentially acting as a token's unique serial number.


**Anti-replay**: By maintaining a list of used jti values, you can prevent replay attacks where a JWT is intercepted and used maliciously by an attacker.

**Token Revocation**: While JWTs are typically stateless and self-contained, sometimes there's a need to revoke them before their expiration (e.g., in case of a token leak). By assigning a unique jti to each token and storing it in a database, you can check tokens against this database to see if they've been revoked.

**Checking jti**:
When verifying a JWT, you can check the jti value to ensure it hasn't been used before (to prevent replay attacks) or that it hasn't been revoked. This typically involves querying a database or cache, so consider the performance implications.

**Duration**:
If you're using the jti claim to prevent replay attacks, you don't need to store the jti value indefinitely. You can discard it after the token's expiration time (exp claim). If you're using it for revocation purposes, you might need to store it longer, depending on your use case.

**Standard Claim**:
The jti claim is a registered claim in the JWT specification (RFC 7519), which means its meaning and usage are defined in the specification, and it's not just a custom claim.

🧠 Remember that while the jti claim can provide some level of protection against replay attacks and can help in token revocation scenarios, it also introduces statefulness to JWTs. Using jti effectively turns the otherwise stateless JWT into a stateful token because you need some external storage (database, cache) to keep track of used or revoked jti values.

#### JWT Authentication Workflow: 

1. User Authentication:
    - The user provides credentials (like a username and password) to the frontend.
    - The frontend sends these credentials to the backend authentication endpoint.

2. Token Generation 
    - The backend verifies the user's credentials.
    - Once verified, the backend generates a JWT. This token typically contains a payload with user information, an expiration time, and other relevant metadata

3. Token Issuance:
    - The backend sends the generated JWT back to the frontend.

4. Storing the JWT
    - The frontend stores the JWT locally, often in an HTTP cookie or in local/session storage.

5. Subsequent Requests
    - For subsequent API requests that require authentication, the frontend attaches the stored JWT in the request headers (often in an "Authorization" header).
    - No need to send username and password again!

6. Token Verification:
    - Upon receiving an API request with an attached JWT, the backend verifies:
        - The JWT signature using the secret key to ensure the token wasn't tampered with.
        - The expiration time of the JWT to make sure it hasn't expired.
    - If the token is valid, the request is processed, and a response is sent back to the frontend. If invalid, an error is returned.

7. Token Refresh (Optional):
    - JWTs often have an expiration time for security reasons. If a token expires, the frontend might need to obtain a new one.
    - There's a common pattern called "refresh tokens" for this. A refresh token is a longer-lived token stored securely on the frontend. If the JWT expires, the frontend uses the refresh token to request a new JWT without requiring the user to log in again. The backend then verifies the validity of the refresh token and issues a new JWT if valid.

8. Logout or Token Revocation:
    - When a user logs out or for any other security reasons (e.g., token compromise), the token should be discarded on the frontend.
    - For enhanced security, especially with refresh tokens, you might maintain a list of valid/revoked tokens on the backend to reject requests bearing revoked tokens.





#### Implementation Guides 
1- Checking Tokens:

 - On each request:
    - Decode the JWT token without verifying (you're just reading the payload).
    - Check the jti or the token itself against your database.
    - If the token is in the database and not marked as revoked, then proceed to verify the token's signature.
    - If verification succeeds, continue processing the request.
    - If the token is revoked or not in the database, or if the verification fails, reject the request.

- Revoking Tokens:
    - To revoke a token, simply mark the revoked flag as true for that token in the database. This will ensure that it's considered invalid during the "Checking Tokens" step, even if its signature is valid and it hasn't expired.


- Cleanup:
    - Periodically, clean up expired tokens from the database, as they're no longer needed.

- Consider Performance:
    - Database checks on every request can introduce a performance overhead. Consider caching mechanisms (storing JWT payload in Redis) to reduce the frequency of direct database hits. For instance, tokens that were recently checked and found valid can be cached to skip the database check for a short period.

- Revoke on Logout:
    - If your application has a logout feature and you want to invalidate the JWT token immediately upon logout, then this setup will be beneficial. Simply mark the token as revoked in the database when the user logs out.


🧠 Remember, this approach is just one way to handle token invalidation. There are other techniques, such as token blacklisting, using short-lived tokens with refresh tokens, or leveraging centralized token introspection endpoints. The best method will depend on your specific needs and constraints.








