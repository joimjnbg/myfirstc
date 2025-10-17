package com.example.autoswiper

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.GestureDescription
import android.graphics.Path
import android.graphics.Point
import android.os.Handler
import android.os.Looper
import android.view.accessibility.AccessibilityEvent
import kotlin.random.Random

class AutoSwipeService : AccessibilityService() {

    private val handler = Handler(Looper.getMainLooper())
    private lateinit var swipeRunnable: Runnable

    companion object {
        var isRunning = false
    }

    override fun onServiceConnected() {
        super.onServiceConnected()
        // Service is connected, but we don't start swiping immediately.
        // isRunning is false by default.
        // We start the runnable loop, but it will wait for isRunning to be true.
        startSwipingLoop()
    }

    private fun startSwipingLoop() {
        swipeRunnable = object : Runnable {
            override fun run() {
                if (isRunning) {
                    performSwipe()
                }
                // Always reschedule to check the isRunning flag again later.
                val delay = if(isRunning) Random.nextLong(1000, 60000) else 500 // Check every 500ms if not running
                handler.postDelayed(this, delay)
            }
        }
        handler.post(swipeRunnable)
    }

    private fun performSwipe() {
        val displayMetrics = resources.displayMetrics
        val width = displayMetrics.widthPixels
        val height = displayMetrics.heightPixels

        // Define margins (10% of screen dimensions)
        val marginX = (width * 0.1).toInt()
        val marginY = (height * 0.1).toInt()

        val path = Path()
        val swipeUp = Random.nextInt(0, 10) >= 1 // 90% chance to swipe up

        if (swipeUp) {
            // SWIPE UP LOGIC (from bottom half)
            val startX = Random.nextInt(marginX, width - marginX)
            val startY = Random.nextInt(height / 2, height - marginY)
            val endX = startX
            val swipeDistance = Random.nextInt((height * 0.2).toInt(), (height * 0.3).toInt())
            val endY = (startY - swipeDistance).coerceAtLeast(marginY)

            path.moveTo(startX.toFloat(), startY.toFloat())
            path.lineTo(endX.toFloat(), endY.toFloat())
        } else {
            // SWIPE DOWN LOGIC (from top half)
            val startX = Random.nextInt(marginX, width - marginX)
            val startY = Random.nextInt(marginY, height / 2)
            val endX = startX
            val swipeDistance = Random.nextInt((height * 0.2).toInt(), (height * 0.3).toInt())
            val endY = (startY + swipeDistance).coerceAtMost(height - marginY)

            path.moveTo(startX.toFloat(), startY.toFloat())
            path.lineTo(endX.toFloat(), endY.toFloat())
        }

        val gesture = GestureDescription.Builder()
            .addStroke(GestureDescription.StrokeDescription(path, 0, 200)) // 200ms duration
            .build()

        dispatchGesture(gesture, null, null)
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        // Not needed for this functionality
    }

    override fun onInterrupt() {
        // Not needed for this functionality
    }



    override fun onDestroy() {
        super.onDestroy()
        handler.removeCallbacks(swipeRunnable)
        isRunning = false
    }
}