import { Button } from "@/components/ui/button"
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import Image from "next/image"
export default function LoginPage() {
    return (
        <div className="mt-0" >

            <Image src="/logo-1615753395.jpg" width={400} height={400} alt="" />
            <Card className="w-full max-w-sm">
                <CardHeader>

                    <CardTitle>Login to your account</CardTitle>
                    <CardDescription>
                        Enter your root username below to login
                    </CardDescription>

                </CardHeader>

                <CardContent>
                    <form>
                        <div className="flex flex-col gap-6">
                            <div className="grid gap-2">
                                <Label htmlFor="email">username</Label>
                                <Input
                                    id="username"
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
                    </form>
                </CardContent>

                <CardFooter className="flex-col gap-2">

                    <Button type="submit" className="w-full login-overlay hover:cursor-pointer">
                        Login
                    </Button>
                </CardFooter>
            </Card>

        </div>
    )
}
