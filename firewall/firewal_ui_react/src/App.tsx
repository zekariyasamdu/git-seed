import { AuthProvider } from "./components/providers/auth-provider"
import { SidebarProvider } from "./components/ui/sidebar"
import Routes from "./routes"
function App() {

  return (
    <SidebarProvider>
      <AuthProvider>
        <Routes />
      </AuthProvider>
    </SidebarProvider>

  )
}

export default App
