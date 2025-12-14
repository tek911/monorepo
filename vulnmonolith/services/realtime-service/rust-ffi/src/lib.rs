//! Rust FFI Library for Realtime Service
//! WARNING: INTENTIONALLY VULNERABLE FOR SECURITY TESTING
//!
//! This library contains intentional vulnerabilities for testing purposes.

use std::ffi::{CStr, CString};
use std::os::raw::{c_char, c_int, c_void};
use std::ptr;
use std::slice;

/// VULNERABILITY: Buffer overflow in parsing
/// CWE-120: Buffer Copy without Checking Size of Input
#[no_mangle]
pub unsafe extern "C" fn parse_data(input: *const c_char, output: *mut c_char, output_len: c_int) -> c_int {
    if input.is_null() || output.is_null() {
        return -1;
    }

    let input_str = CStr::from_ptr(input);
    let input_bytes = input_str.to_bytes();

    // VULNERABILITY: No bounds checking - buffer overflow possible
    // If input is larger than output_len, this overflows
    ptr::copy_nonoverlapping(
        input_bytes.as_ptr(),
        output as *mut u8,
        input_bytes.len(), // Should check against output_len
    );

    input_bytes.len() as c_int
}

/// VULNERABILITY: Use after free
/// CWE-416: Use After Free
#[no_mangle]
pub unsafe extern "C" fn process_and_free(data: *mut c_void, size: usize) -> c_int {
    if data.is_null() {
        return -1;
    }

    // Create a Box from the raw pointer
    let boxed = Box::from_raw(data as *mut u8);

    // Free the memory
    drop(boxed);

    // VULNERABILITY: Use after free - accessing freed memory
    let slice = slice::from_raw_parts(data as *const u8, size);
    let sum: u8 = slice.iter().sum();

    sum as c_int
}

/// VULNERABILITY: Double free
/// CWE-415: Double Free
static mut FREED_PTR: *mut c_void = ptr::null_mut();

#[no_mangle]
pub unsafe extern "C" fn double_free_vuln(ptr: *mut c_void) {
    if !ptr.is_null() {
        // First free
        let _ = Box::from_raw(ptr as *mut u8);

        // Store for later double free
        FREED_PTR = ptr;
    }
}

#[no_mangle]
pub unsafe extern "C" fn trigger_double_free() {
    // VULNERABILITY: Double free - freeing already freed memory
    if !FREED_PTR.is_null() {
        let _ = Box::from_raw(FREED_PTR as *mut u8);
    }
}

/// VULNERABILITY: Integer overflow
/// CWE-190: Integer Overflow or Wraparound
#[no_mangle]
pub extern "C" fn allocate_buffer(count: c_int, size: c_int) -> *mut c_void {
    // VULNERABILITY: Integer overflow in multiplication
    // count * size can overflow, leading to small allocation
    let total_size = (count as usize) * (size as usize);

    // If overflow occurred, total_size is smaller than expected
    let mut buffer = Vec::with_capacity(total_size);
    let ptr = buffer.as_mut_ptr();
    std::mem::forget(buffer);

    ptr as *mut c_void
}

/// VULNERABILITY: Format string (simulated via unsafe string handling)
#[no_mangle]
pub unsafe extern "C" fn format_message(format: *const c_char, arg: *const c_char) -> *mut c_char {
    if format.is_null() {
        return ptr::null_mut();
    }

    let format_str = CStr::from_ptr(format).to_string_lossy();
    let arg_str = if arg.is_null() {
        String::new()
    } else {
        CStr::from_ptr(arg).to_string_lossy().into_owned()
    };

    // VULNERABILITY: User-controlled format string
    let result = format_str.replace("{}", &arg_str);

    CString::new(result).unwrap().into_raw()
}

/// VULNERABILITY: Memory leak
/// CWE-401: Missing Release of Memory after Effective Lifetime
#[no_mangle]
pub extern "C" fn create_connection() -> *mut c_void {
    // VULNERABILITY: Allocated memory never freed (intentional leak)
    let connection = Box::new(vec![0u8; 1024]);
    Box::into_raw(connection) as *mut c_void
    // No corresponding free function provided
}

/// VULNERABILITY: Null pointer dereference
/// CWE-476: NULL Pointer Dereference
#[no_mangle]
pub unsafe extern "C" fn unsafe_deref(ptr: *const c_int) -> c_int {
    // VULNERABILITY: No null check before dereference
    *ptr
}

/// VULNERABILITY: Out of bounds read
/// CWE-125: Out-of-bounds Read
#[no_mangle]
pub unsafe extern "C" fn read_at_index(arr: *const c_int, len: c_int, index: c_int) -> c_int {
    // VULNERABILITY: No bounds checking
    let slice = slice::from_raw_parts(arr, len as usize);

    // Index could be >= len, causing out of bounds read
    slice[index as usize]
}

/// VULNERABILITY: Uninitialized memory
/// CWE-908: Use of Uninitialized Resource
#[no_mangle]
pub extern "C" fn get_uninitialized_buffer(size: usize) -> *mut u8 {
    // VULNERABILITY: Returning uninitialized memory
    let mut buffer: Vec<u8> = Vec::with_capacity(size);
    unsafe {
        buffer.set_len(size); // Memory is uninitialized!
    }
    let ptr = buffer.as_mut_ptr();
    std::mem::forget(buffer);
    ptr
}

/// VULNERABILITY: Race condition in static mutable
/// CWE-362: Race Condition
static mut GLOBAL_COUNTER: i32 = 0;

#[no_mangle]
pub unsafe extern "C" fn increment_counter() -> i32 {
    // VULNERABILITY: Race condition on static mutable
    GLOBAL_COUNTER += 1;
    GLOBAL_COUNTER
}

#[no_mangle]
pub unsafe extern "C" fn get_counter() -> i32 {
    // VULNERABILITY: Unsynchronized read
    GLOBAL_COUNTER
}
