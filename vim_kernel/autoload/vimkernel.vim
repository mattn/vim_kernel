function! s:encode(str) abort
  let str = a:str
  let str = substitute(str, '&', '\&amp;', 'g')
  let str = substitute(str, '>', '\&gt;', 'g')
  let str = substitute(str, '<', '\&lt;', 'g')
  let str = substitute(str, "\n", '\&#x0d;', 'g')
  let str = substitute(str, '"', '\&quot;', 'g')
  let str = substitute(str, "'", '\&apos;', 'g')
  let str = substitute(str, ' ', '\&nbsp;', 'g')
  return str
endfunction

function! vimkernel#display_table(data)
  let l:table = '<table border=1>'
  for l:row in a:data
    let l:table .= '<tr>'
    for l:col in l:row
      let l:str = type(l:col) == v:t_string ? l:col : string(l:col)
      let l:table .= '<td>' . s:encode(l:str) . '</td>'
    endfor
    let l:table .= '</tr>'
  endfor
  let l:table .= '</table>'
  let g:vimkernel_display_data = {
  \  'source': 'kernel',
  \  'data': {
  \    'text/html': l:table,
  \    'text/plain': string(a:data),
  \  },
  \	 'metadata': {},
  \}
endfunction
