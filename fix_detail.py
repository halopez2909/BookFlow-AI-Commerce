with open("frontend-bookflow/src/hooks/useBookDetail.ts", "r", encoding="utf-8") as f:
    content = f.read()

# Add book alias to the return
content = content.replace(
    "    enabled: !!bookId,\n    staleTime: 1000 * 60,\n    retry: 1,\n  })\n}",
    "    enabled: !!bookId,\n    staleTime: 1000 * 60,\n    retry: 1,\n  })\n  const q = useQuery<Book, Error>({\n    queryKey: ['catalog', 'books', bookId],\n    queryFn: async () => {\n      const { data } = await api.get('/api/catalog/books/' + bookId)\n      return data\n    },\n    enabled: !!bookId,\n    staleTime: 1000 * 60,\n    retry: 1,\n  })\n  return { book: q.data, isLoading: q.isLoading, isError: q.isError }\n}"
)

with open("frontend-bookflow/src/hooks/useBookDetail.ts", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
