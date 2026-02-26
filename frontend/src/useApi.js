import { useState } from "react";

export function useApi() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const request = async (path) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(path);
      const text = await res.text();
      let data;
      try {
        data = JSON.parse(text);
      } catch {
        data = text;
      }
      if (!res.ok) {
        throw new Error(
          `${res.status} ${res.statusText}: ${
            typeof data === "string" ? data : JSON.stringify(data)
          }`
        );
      }
      return data;
    } catch (e) {
      setError(e.message);
      throw e;
    } finally {
      setLoading(false);
    }
  };

  return { request, loading, error };
}