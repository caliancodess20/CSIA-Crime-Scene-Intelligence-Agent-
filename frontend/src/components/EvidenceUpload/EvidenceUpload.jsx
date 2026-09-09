import { useState, useRef } from 'react'
import { UploadCloud, FileImage, FileText, Video, Check } from 'lucide-react'
import { uploadEvidence } from '../../api/evidence'

const iconFor = {
  image: FileImage,
  video_frame: Video,
  text: FileText
}

export default function EvidenceUpload({ caseId }) {
  const [dragOver, setDragOver] = useState(false)
  const [queue, setQueue] = useState([]) // { file, progress, result }
  const inputRef = useRef(null)

  function handleFiles(fileList) {
    const files = Array.from(fileList)
    files.forEach((file) => {
      const entry = { id: `${file.name}-${Date.now()}`, file, progress: 0, result: null }
      setQueue((q) => [...q, entry])
      uploadEvidence(caseId, file, (pct) => {
        setQueue((q) => q.map((e) => (e.id === entry.id ? { ...e, progress: pct } : e)))
      }).then((result) => {
        setQueue((q) => q.map((e) => (e.id === entry.id ? { ...e, progress: 100, result } : e)))
      })
    })
  }

  return (
    <div className="space-y-4">
      <div
        onDragOver={(e) => {
          e.preventDefault()
          setDragOver(true)
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={(e) => {
          e.preventDefault()
          setDragOver(false)
          handleFiles(e.dataTransfer.files)
        }}
        onClick={() => inputRef.current?.click()}
        className={`flex cursor-pointer flex-col items-center justify-center gap-2 rounded-sm border-2 border-dashed p-10 text-center transition-colors ${
          dragOver ? 'border-tag-amber bg-tag-amber/5' : 'border-ink-600 hover:border-ink-500'
        }`}
      >
        <UploadCloud size={28} className="text-text-faint" />
        <p className="text-sm text-text-primary">Drop image, video frame, or statement files here</p>
        <p className="text-xs text-text-faint">or click to browse — routed to Vision, OCR, and NLP by file type</p>
        <input
          ref={inputRef}
          type="file"
          multiple
          className="hidden"
          onChange={(e) => e.target.files && handleFiles(e.target.files)}
        />
      </div>

      {queue.length > 0 && (
        <ul className="space-y-2">
          {queue.map((entry) => {
            const Icon = iconFor[entry.result?.type] ?? FileText
            return (
              <li
                key={entry.id}
                className="flex items-center gap-3 rounded-sm border border-ink-700 bg-ink-800 px-3 py-2"
              >
                <Icon size={16} className="shrink-0 text-text-faint" />
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm text-text-primary">{entry.file.name}</p>
                  <div className="mt-1 h-1 w-full overflow-hidden rounded-full bg-ink-600">
                    <div
                      className="h-full bg-tag-amber transition-all"
                      style={{ width: `${entry.progress}%` }}
                    />
                  </div>
                </div>
                {entry.progress === 100 ? (
                  <Check size={16} className="shrink-0 text-tag-moss" />
                ) : (
                  <span className="shrink-0 font-mono text-xs text-text-faint">{entry.progress}%</span>
                )}
              </li>
            )
          })}
        </ul>
      )}
    </div>
  )
}
