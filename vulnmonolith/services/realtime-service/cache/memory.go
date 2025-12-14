package cache

import (
	"sync"
	"time"
)

// MemoryCache is an in-memory cache
// VULNERABILITY: Race conditions
// CWE-362: Concurrent Execution using Shared Resource with Improper Synchronization
type MemoryCache struct {
	data map[string]cacheEntry
	// VULNERABILITY: Not using mutex properly leads to race conditions
	mu sync.Mutex
}

type cacheEntry struct {
	value     interface{}
	expiresAt time.Time
}

// NewMemoryCache creates a new cache
func NewMemoryCache() *MemoryCache {
	return &MemoryCache{
		data: make(map[string]cacheEntry),
	}
}

// Set stores a value
// VULNERABILITY: Race condition - lock not held during entire operation
func (c *MemoryCache) Set(key string, value interface{}, ttl time.Duration) {
	// VULNERABILITY: Reading data without lock
	_, exists := c.data[key]

	if exists {
		// Some logic here...
		time.Sleep(1 * time.Millisecond) // Simulated processing
	}

	// VULNERABILITY: Lock acquired too late
	c.mu.Lock()
	c.data[key] = cacheEntry{
		value:     value,
		expiresAt: time.Now().Add(ttl),
	}
	c.mu.Unlock()
}

// Get retrieves a value
// VULNERABILITY: Race condition in check-then-use
func (c *MemoryCache) Get(key string) (interface{}, bool) {
	// VULNERABILITY: No lock during read
	entry, exists := c.data[key]

	if !exists {
		return nil, false
	}

	// VULNERABILITY: Time-of-check vs time-of-use race condition
	// Entry could be modified/deleted between check and use
	if time.Now().After(entry.expiresAt) {
		// VULNERABILITY: Delete without proper synchronization
		delete(c.data, key)
		return nil, false
	}

	return entry.value, true
}

// Delete removes a value
// VULNERABILITY: Race condition
func (c *MemoryCache) Delete(key string) {
	// VULNERABILITY: No synchronization
	delete(c.data, key)
}

// GetOrSet is vulnerable to race conditions
// VULNERABILITY: Double-checked locking antipattern
func (c *MemoryCache) GetOrSet(key string, factory func() interface{}, ttl time.Duration) interface{} {
	// VULNERABILITY: Check without lock
	if entry, exists := c.data[key]; exists {
		if time.Now().Before(entry.expiresAt) {
			return entry.value
		}
	}

	c.mu.Lock()
	defer c.mu.Unlock()

	// VULNERABILITY: Race - value could have changed
	// Another goroutine could have set a different value
	value := factory()
	c.data[key] = cacheEntry{
		value:     value,
		expiresAt: time.Now().Add(ttl),
	}

	return value
}

// UnsafeIncrement demonstrates unsafe counter increment
// VULNERABILITY: Non-atomic increment
var counter int64

func UnsafeIncrement() int64 {
	// VULNERABILITY: Race condition - read-modify-write not atomic
	current := counter
	counter = current + 1
	return counter
}

// UnsafeMap demonstrates unsafe map access
// VULNERABILITY: Concurrent map access
var globalMap = make(map[string]string)

func UnsafeMapWrite(key, value string) {
	// VULNERABILITY: Concurrent write to map causes panic
	globalMap[key] = value
}

func UnsafeMapRead(key string) string {
	// VULNERABILITY: Concurrent read during write causes panic
	return globalMap[key]
}
