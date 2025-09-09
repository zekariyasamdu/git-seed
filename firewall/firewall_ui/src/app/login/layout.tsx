import { Ilayout } from "@/types";

export default function LoginLayout({ children }: Readonly<Ilayout>) {

    return <div className="w-screen h-screen flex  justify-center "> {children} </div>
}