import "server-only"
import { jwtVerify, SignJWT } from "jose"
import { cookies } from "next/headers";

const secretKey = "1234";
const encodedKey = new TextEncoder().encode(secretKey);

type SessionPayload = {
    userId: string;
    expiresAt: Date;
}

export async function createSession(userId: string) {
    const expiresAt = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)

    const session = await encrypt({ userId, expiresAt })

        ; (await cookies()).set("session", session, {
            httpOnly: true,
            secure: true,
            expires: expiresAt,
            sameSite: "lax",
            path: "/"
        })
}

export async function deleleSession() {
    (await cookies()).delete("session");
}


export async function encrypt(payload: SessionPayload): Promise<string> {
    return new SignJWT(payload)
        .setProtectedHeader({ alg: "HS256" })
        .setIssuedAt()
        .setExpirationTime("7d")
        .sign(encodedKey)
}

export async function decrypt(session: string | undefined = "") {
    try {
        const { payload } = await jwtVerify(session, encodedKey, {
            algorithms: ["HS256"]
        })
        return payload
    }
    catch (e) {
        console.error("error", e)
    }

}
