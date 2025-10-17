package com.example.autoswiper

import android.accessibilityservice.AccessibilityServiceInfo
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.provider.Settings
import android.view.accessibility.AccessibilityManager
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private lateinit var serviceButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        serviceButton = findViewById(R.id.service_button)

        serviceButton.setOnClickListener {
            if (isAccessibilityServiceEnabled()) {
                // Toggle the running state of the service's action
                AutoSwipeService.isRunning = !AutoSwipeService.isRunning
                updateButtonState()
            } else {
                // Request permission if not enabled
                val intent = Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)
                startActivity(intent)
            }
        }
    }

    override fun onResume() {
        super.onResume()
        updateButtonState()
    }

    private fun isAccessibilityServiceEnabled(): Boolean {
        val am = getSystemService(Context.ACCESSIBILITY_SERVICE) as AccessibilityManager
        val enabledServices = am.getEnabledAccessibilityServiceList(AccessibilityServiceInfo.FEEDBACK_ALL_MASK)
        return enabledServices.any { it.id == packageName + "/.AutoSwipeService" }
    }

    private fun updateButtonState() {
        if (isAccessibilityServiceEnabled()) {
            if (AutoSwipeService.isRunning) {
                serviceButton.text = "Stop Swiping"
            } else {
                serviceButton.text = "Start Swiping"
            }
        } else {
            serviceButton.text = "Enable Service in Settings"
        }
    }
}