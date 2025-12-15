package handlers

import (
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"path/filepath"
)

// FileHandler handles file operations
// VULNERABILITY: Path Traversal
// CWE-22: Path Traversal
func FileHandler(w http.ResponseWriter, r *http.Request) {
	action := r.URL.Query().Get("action")
	filename := r.URL.Query().Get("file")

	baseDir := "/var/data/"

	switch action {
	case "read":
		// VULNERABILITY: Path traversal - no sanitization
		// Attack: file=../../../etc/passwd
		filePath := baseDir + filename

		content, err := ioutil.ReadFile(filePath)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.Write(content)

	case "write":
		content := r.URL.Query().Get("content")
		// VULNERABILITY: Arbitrary file write
		filePath := baseDir + filename

		err := ioutil.WriteFile(filePath, []byte(content), 0644)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.Write([]byte("File written"))

	case "delete":
		// VULNERABILITY: Arbitrary file deletion
		filePath := baseDir + filename
		os.Remove(filePath)
		w.Write([]byte("File deleted"))

	case "list":
		// VULNERABILITY: Directory traversal in listing
		dirPath := baseDir + filename
		files, _ := ioutil.ReadDir(dirPath)
		for _, f := range files {
			fmt.Fprintf(w, "%s\n", f.Name())
		}
	}
}

// DownloadHandler handles file downloads
// VULNERABILITY: Path Traversal
func DownloadHandler(w http.ResponseWriter, r *http.Request) {
	filename := r.URL.Query().Get("file")

	// VULNERABILITY: No path validation
	filePath := filepath.Join("/var/downloads", filename)

	file, err := os.Open(filePath)
	if err != nil {
		http.Error(w, "File not found", http.StatusNotFound)
		return
	}
	defer file.Close()

	// VULNERABILITY: No content-type validation
	w.Header().Set("Content-Disposition", fmt.Sprintf("attachment; filename=%s", filename))
	io.Copy(w, file)
}

// UploadHandler handles file uploads
// VULNERABILITY: Unrestricted file upload
func UploadHandler(w http.ResponseWriter, r *http.Request) {
	r.ParseMultipartForm(100 << 20) // 100MB max

	file, handler, err := r.FormFile("file")
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	defer file.Close()

	// VULNERABILITY: Using user-provided filename directly
	filename := handler.Filename

	// VULNERABILITY: No file type validation
	// VULNERABILITY: Path traversal possible in filename
	destPath := filepath.Join("/var/uploads", filename)

	dst, err := os.Create(destPath)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer dst.Close()

	io.Copy(dst, file)
	w.Write([]byte("Upload successful: " + filename))
}

// SymlinkHandler handles symlink creation
// VULNERABILITY: Symlink attack
func SymlinkHandler(w http.ResponseWriter, r *http.Request) {
	target := r.URL.Query().Get("target")
	link := r.URL.Query().Get("link")

	// VULNERABILITY: Creating arbitrary symlinks
	// Can link to sensitive files
	err := os.Symlink(target, filepath.Join("/var/data", link))
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Write([]byte("Symlink created"))
}

// TempFileHandler demonstrates insecure temp file handling
// VULNERABILITY: Insecure temporary file creation
func TempFileHandler(w http.ResponseWriter, r *http.Request) {
	prefix := r.URL.Query().Get("prefix")

	// VULNERABILITY: Predictable temp file location
	// VULNERABILITY: User-controlled prefix
	tmpFile := fmt.Sprintf("/tmp/%s_%d", prefix, os.Getpid())

	err := ioutil.WriteFile(tmpFile, []byte("temp data"), 0666) // VULNERABILITY: World-writable
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Write([]byte("Temp file: " + tmpFile))
}
