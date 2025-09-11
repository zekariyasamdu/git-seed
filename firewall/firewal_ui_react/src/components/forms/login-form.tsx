"use client"
import { login } from "@/auth"
import { Button } from "@/components/ui/button"
import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useActionState } from "react"


export default function LoginForm() {
    const [data, loginAction, pending] = useActionState(login, undefined)

    return (
        <div className="mt-0 flex flex-col items-center" >
            <img src="/src/assets/logo-1615753395.jpg" width={400} height={400} alt="" />
            <Card className="w-full max-w-sm ">
                <form action={loginAction}>
                    <CardHeader>

                        {data?.error?.adminName && (
                            <Label className="text-red-500">{data.error.adminName}</Label>
                        )}

                    </CardHeader>

                    <CardContent>
                        <div className="flex flex-col gap-6">
                            <div className="grid gap-2">
                                <Label htmlFor="email">username</Label>
                                <Input
                                    id="adminname"
                                    type="text"
                                    placeholder="root"
                                    required
                                />
                            </div>
                            <div className="grid gap-2">
                                <Label htmlFor="password">Password</Label>
                                <Input id="password" type="password" required />
                            </div>
                        </div>

                    </CardContent>

                    <CardFooter className="flex-col gap-2 mt-4">
                        <Button disabled={pending} type="submit" className="w-full login-overlay hover:cursor-pointer" > login </Button>
                    </CardFooter>
                </form>
            </Card>
        </div>
    )
}