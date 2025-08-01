'use client';
import { AppUser, AuthContextType } from "@/components/context-provider/auth-provider";
import { useRouter } from "next/navigation"; // 
import { useState } from "react";

export default function useFetchAuth() {
  const [loading, setLoading] = useState<boolean>(false);
  const [user, setUser] = useState<AppUser | null>(null);
  const router = useRouter();

  const login = async (email: string, password: string) => {
    try {
      setLoading(true);
      const res = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', 
        },
        body: JSON.stringify({ email, password }),
      });

      if (res.status !== 200) {
        throw new Error("Invalid credentials");
      }

      const data: AppUser = await res.json();
      setUser(data);
      router.push('/dashboard'); 
    } catch (e) {
      console.error('Login error', e);
    } finally {
      setLoading(false);
    }
  };

  const register = async (email: string, password: string) => {
    try {
      setLoading(true);
      const res = await fetch('http://localhost:5000/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', 
        },
        body: JSON.stringify({ email, password }),
      });

      if (res.status !== 201) {
        throw new Error("Registration failed");
      }

      router.push('/login');
    } catch (e) {
      console.error('Register error', e);
    } finally {
      setLoading(false);
    }
  };

  const signout = () => {
    setUser(null);
    router.push('/login');
  };

  const authInfo: AuthContextType = { user, loading, login, register, signout };
  return authInfo;
}
