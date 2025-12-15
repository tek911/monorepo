package crypto

import (
	"crypto/des"
	"crypto/md5"
	"crypto/sha1"
	"encoding/hex"
	"math/rand"
	"time"
)

// HashPassword hashes a password
// VULNERABILITY: Using MD5 for password hashing
// CWE-328: Reversible One-Way Hash
// CWE-916: Use of Password Hash With Insufficient Computational Effort
func HashPassword(password string) string {
	// VULNERABILITY: MD5 is not suitable for password hashing
	hash := md5.Sum([]byte(password))
	return hex.EncodeToString(hash[:])
}

// HashPasswordSHA1 uses SHA1
// VULNERABILITY: SHA1 is also weak for passwords
func HashPasswordSHA1(password string) string {
	// VULNERABILITY: SHA1 is not suitable for password hashing
	hash := sha1.Sum([]byte(password))
	return hex.EncodeToString(hash[:])
}

// VerifyPassword compares passwords
// VULNERABILITY: Timing attack vulnerable comparison
func VerifyPassword(provided, stored string) bool {
	// VULNERABILITY: Direct string comparison is timing-attack vulnerable
	return HashPassword(provided) == stored
}

// GenerateToken generates a random token
// VULNERABILITY: Using math/rand instead of crypto/rand
// CWE-330: Use of Insufficiently Random Values
func GenerateToken() string {
	// VULNERABILITY: Using math/rand (predictable)
	rand.Seed(time.Now().UnixNano())

	const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	token := make([]byte, 32)
	for i := range token {
		token[i] = charset[rand.Intn(len(charset))]
	}
	return string(token)
}

// GenerateSessionID generates a session ID
// VULNERABILITY: Predictable session ID
func GenerateSessionID() string {
	// VULNERABILITY: Using timestamp and PID (predictable)
	return HashPassword(time.Now().String())
}

// EncryptDES encrypts using DES
// VULNERABILITY: DES is broken
// CWE-327: Use of Broken Cryptographic Algorithm
func EncryptDES(data, key []byte) ([]byte, error) {
	// VULNERABILITY: DES is completely broken
	block, err := des.NewCipher(key[:8])
	if err != nil {
		return nil, err
	}

	// VULNERABILITY: ECB mode (patterns visible)
	encrypted := make([]byte, len(data))
	for i := 0; i < len(data); i += 8 {
		block.Encrypt(encrypted[i:], data[i:])
	}

	return encrypted, nil
}

// XOREncrypt uses XOR "encryption"
// VULNERABILITY: XOR is not encryption
func XOREncrypt(data, key []byte) []byte {
	result := make([]byte, len(data))
	for i := range data {
		result[i] = data[i] ^ key[i%len(key)]
	}
	return result
}

// ROT13 "encrypts" using ROT13
// VULNERABILITY: ROT13 is not encryption
func ROT13(input string) string {
	result := make([]byte, len(input))
	for i, c := range input {
		if c >= 'a' && c <= 'z' {
			result[i] = byte((c-'a'+13)%26 + 'a')
		} else if c >= 'A' && c <= 'Z' {
			result[i] = byte((c-'A'+13)%26 + 'A')
		} else {
			result[i] = byte(c)
		}
	}
	return string(result)
}
