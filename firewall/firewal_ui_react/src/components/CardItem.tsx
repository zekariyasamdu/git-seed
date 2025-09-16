import { Card, CardContent, CardDescription, CardTitle } from "./ui/card";

type ICardItem = {
    title: string
    content: string
    description: string
    warning: boolean
} & React.HTMLAttributes<HTMLDivElement>


export default function CardItem({ title, content, description, warning = false, ...props }: ICardItem) {
    return (

        <Card {...props}>
            <CardTitle className={`absolute left-3 top-3 ${!warning ? "text-gray-500" : "text-red-600"}`}> {title}</CardTitle>
            <CardContent className="text-6xl">{content}</CardContent>
            <CardDescription className="text-gray-500">{description}</CardDescription>
        </Card>

    )
}