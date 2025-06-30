import htmx from 'htmx.org';
export function copyShortUrl() {
  return {
    fullUrl: '',
    async copy() {
      this.fullUrl = `${this.$refs.prefix.textContent.trim()}${this.$refs.code.value}`;
      await navigator.clipboard.writeText(this.fullUrl);
      htmx.ajax('GET', this.$el.dataset.copySuccess, {
        target: '#messages',      // 將回傳結果插入此容器
        swap: 'innerHTML',        // 只替換內容，不替換整個元素
      });
    }
  };
}
