let s:base = expand('<sfile>:p:h')

function! s:watch_stdin(...) abort
  let l:input = s:base . '/' . getpid() . '.input'
  while 1
    sleep 500m
    if !filereadable(l:input)
      continue
    endif
    try
      let g:vimkernel_display_data = v:none
      let l:stderr = ''
      redir => l:stdout
      exe 'source' l:input
    catch
      let l:stderr = v:exception
    finally
      redir END
      if &filetype == 'help'
        let l:l1 = line('.')
        silent normal! j
        silent let l:l2 = search('\*[^*]\+\*$', 'W')
        if l:l2 == 0
          let l:l2 = line('$')
        else
          let l:l2 -= 1
        endif
        let l:lines = getline(l:l1, l:l2)
        let l:stdout = join(l:lines, "\n")
        close
      endif
      if !empty(l:stdout) && l:stdout[0] == "\n"
        let l:stdout = l:stdout[1:]
      endif
      call delete(l:input)
      let l:temp = s:base . '/' . getpid() . '.temp'
      let l:res = {
      \  'stdout': l:stdout,
      \  'stderr': l:stderr
      \}
      if !empty(g:vimkernel_display_data)
        let l:res['data'] = g:vimkernel_display_data
      endif
      call writefile([json_encode(l:res)], l:temp)
      let l:output = s:base . '/' . getpid() . '.output'
      call rename(l:temp, l:output)
    endtry
  endwhile
endfunction

set encoding=utf-8
exe 'set rtp+=' . s:base
"call timer_start(500, function('s:watch_stdin'), {'repeat': -1})
call s:watch_stdin()
