export const getUrlWithParams = (path: string, searchParams?: URLSearchParams | null) => {
  const currentParams = searchParams?.toString();
  return currentParams ? `${path}?${currentParams}` : path;
};