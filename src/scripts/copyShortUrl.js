export function copyShortUrl() {
  return {
    fullUrl: '',
    async copy() {
      this.fullUrl = `${this.$refs.prefix.textContent.trim()}${this.$refs.code.value}`;
      try {
        await navigator.clipboard.writeText(this.fullUrl);
      } catch (e) {
        console.error('複製失敗', e);
      }
    }
  };
}
