(function () {
  'use strict'

  function getCookie(name) {
    const cookie = document.cookie
      .split(';')
      .map(item => item.trim())
      .find(item => item.startsWith(`${name}=`))
    return cookie ? decodeURIComponent(cookie.slice(name.length + 1)) : ''
  }

  function markdownAltText(filename) {
    return filename
      .replace(/\.[^.]+$/, '')
      .replace(/[\[\]\\]/g, '')
      .trim()
  }

  function insertAtCursor(textarea, markdown) {
    const start = textarea.selectionStart ?? textarea.value.length
    const end = textarea.selectionEnd ?? start
    const before = textarea.value.slice(0, start)
    const after = textarea.value.slice(end)
    const prefix = before && !before.endsWith('\n\n')
      ? (before.endsWith('\n') ? '\n' : '\n\n')
      : ''
    const suffix = after && !after.startsWith('\n\n')
      ? (after.startsWith('\n') ? '\n' : '\n\n')
      : ''
    const inserted = `${prefix}${markdown}${suffix}`

    textarea.setRangeText(inserted, start, end, 'end')
    textarea.dispatchEvent(new Event('input', { bubbles: true }))
    textarea.dispatchEvent(new Event('change', { bubbles: true }))
    textarea.focus()
  }

  function enhanceTextarea(textarea) {
    if (textarea.dataset.imageWidgetReady === 'true') return
    textarea.dataset.imageWidgetReady = 'true'

    const toolbar = document.createElement('div')
    toolbar.className = 'markdown-image-toolbar'

    const button = document.createElement('button')
    button.type = 'button'
    button.className = 'markdown-image-upload-button'
    button.textContent = '上传并插入图片'

    const hint = document.createElement('span')
    hint.className = 'markdown-image-hint'
    hint.textContent = '支持 JPG、PNG、GIF、WebP，最大 10 MB'

    const status = document.createElement('span')
    status.className = 'markdown-image-status'
    status.setAttribute('role', 'status')
    status.setAttribute('aria-live', 'polite')

    const input = document.createElement('input')
    input.type = 'file'
    input.accept = 'image/jpeg,image/png,image/gif,image/webp'
    input.hidden = true

    toolbar.append(button, hint, status, input)
    textarea.parentNode.insertBefore(toolbar, textarea)

    button.addEventListener('click', () => input.click())
    input.addEventListener('change', async () => {
      const file = input.files && input.files[0]
      if (!file) return

      const maxSize = Number(textarea.dataset.maxImageSize || 10 * 1024 * 1024)
      if (file.size > maxSize) {
        status.textContent = '图片不能超过 10 MB'
        status.dataset.state = 'error'
        input.value = ''
        return
      }

      button.disabled = true
      status.textContent = '正在上传…'
      status.dataset.state = 'loading'

      const formData = new FormData()
      formData.append('image', file)
      formData.append('alt_text', markdownAltText(file.name))

      try {
        const response = await fetch(textarea.dataset.imageUploadUrl, {
          method: 'POST',
          credentials: 'same-origin',
          headers: { 'X-CSRFToken': getCookie('csrftoken') },
          body: formData,
        })
        const data = await response.json()
        if (!response.ok) throw new Error(data.error || '上传失败')

        const altText = data.alt_text || markdownAltText(file.name) || '文章图片'
        insertAtCursor(textarea, `![${altText}](${data.url})`)
        status.textContent = '图片已插入正文'
        status.dataset.state = 'success'
      } catch (error) {
        status.textContent = error.message || '上传失败，请重试'
        status.dataset.state = 'error'
      } finally {
        button.disabled = false
        input.value = ''
      }
    })
  }

  function init() {
    document
      .querySelectorAll('textarea[data-image-upload-url]')
      .forEach(enhanceTextarea)
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init)
  } else {
    init()
  }
})()
