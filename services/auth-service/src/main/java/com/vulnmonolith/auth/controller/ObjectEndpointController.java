package com.vulnmonolith.auth.controller;

import com.vulnmonolith.auth.model.UserSession;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.*;
import java.util.Base64;

/**
 * VULNERABILITY: Insecure Deserialization endpoints
 * CWE-502: Deserialization of Untrusted Data
 */
@RestController
@RequestMapping("/api/session")
public class ObjectEndpointController {

    /**
     * VULNERABILITY: Insecure deserialization of user-supplied data
     * Accepts base64-encoded serialized Java objects
     */
    @PostMapping("/restore")
    public ResponseEntity<?> restoreSession(@RequestBody String serializedData) {
        try {
            // VULNERABILITY: Deserializing untrusted data
            byte[] data = Base64.getDecoder().decode(serializedData);
            ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));

            // VULNERABILITY: No type checking before deserialization
            UserSession session = (UserSession) ois.readObject();
            ois.close();

            return ResponseEntity.ok(session);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Failed to restore session: " + e.getMessage());
        }
    }

    /**
     * VULNERABILITY: Another deserialization endpoint accepting raw bytes
     */
    @PostMapping(value = "/restore-binary", consumes = "application/octet-stream")
    public ResponseEntity<?> restoreSessionBinary(@RequestBody byte[] data) {
        try {
            // VULNERABILITY: Direct deserialization of binary data
            ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
            Object obj = ois.readObject();
            ois.close();

            if (obj instanceof UserSession) {
                return ResponseEntity.ok(obj);
            }
            return ResponseEntity.badRequest().body("Invalid session object");
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Deserialization failed: " + e.getMessage());
        }
    }

    /**
     * Serialize session - helper for creating payloads
     */
    @PostMapping("/save")
    public ResponseEntity<?> saveSession(@RequestBody UserSession session) {
        try {
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            ObjectOutputStream oos = new ObjectOutputStream(baos);
            oos.writeObject(session);
            oos.close();

            String encoded = Base64.getEncoder().encodeToString(baos.toByteArray());
            return ResponseEntity.ok(encoded);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Serialization failed");
        }
    }

    /**
     * VULNERABILITY: Deserialization with YAML (SnakeYAML vulnerability)
     */
    @PostMapping(value = "/restore-yaml", consumes = "application/x-yaml")
    public ResponseEntity<?> restoreSessionYaml(@RequestBody String yamlData) {
        try {
            // VULNERABILITY: Unsafe YAML deserialization
            org.yaml.snakeyaml.Yaml yaml = new org.yaml.snakeyaml.Yaml();
            Object obj = yaml.load(yamlData);
            return ResponseEntity.ok(obj);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("YAML parsing failed: " + e.getMessage());
        }
    }
}
