package com.rozetkin.ugraquest

// toasts
//okhttp
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.os.Environment
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.core.content.FileProvider
import androidx.fragment.app.Fragment
import okhttp3.*
import okio.IOException
import java.io.File

// TODO: Rename parameter arguments, choose names that match
// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val ARG_PARAM1 = "param1"
private const val ARG_PARAM2 = "param2"


/**
 * A simple [Fragment] subclass.
 * Use the [QuestionFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class QuestionFragment : Fragment() {
    // TODO: Rename and change types of parameters
    private var param1: String? = null
    private var param2: String? = null
    private var qTotal: Int? = null // total number of questions


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d(TAG, "onCreate")
        arguments?.let {
            param1 = it.getString(ARG_PARAM1)
            param2 = it.getString(ARG_PARAM2)
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        Log.d(TAG, "onCreateView")
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_question, container, false)
    }


    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        qTotal = view.resources.getInteger(R.integer.qTotal)

        Log.d(TAG, "onViewCreated")
        view.findViewById<Button>(R.id.button_ans_1).setOnClickListener {
            updateState(view, "1")
        }
        view.findViewById<Button>(R.id.button_ans_2).setOnClickListener {
            updateState(view, "2")
        }
        view.findViewById<Button>(R.id.button_ans_3).setOnClickListener {
            updateState(view, "3")
        }

        updateState(view, "")

    }

    fun updateState(view: View, newState: String) {
        state += newState
        qNum = qNum + 1

        // get question from resources by id question_$qNum



        if (qNum <= qTotal!!) {
            val question = view.resources.getStringArray(view.resources.getIdentifier("question_$qNum", "array", view.context.packageName))
            view.findViewById<TextView>(R.id.text_question).text = question[0]
            view.findViewById<Button>(R.id.button_ans_1).text = question[1]
            view.findViewById<Button>(R.id.button_ans_2).text = question[2]
            view.findViewById<Button>(R.id.button_ans_3).text = question[3]
            val right_ans = question[4]
            if (newState == right_ans) {
                // Cool, but there is serverside validation
                view.findViewById<Button>(R.id.button_ans_3).text = question[3]
            }
        }
        else{
            // text from resources and placeholders
            view.findViewById<TextView>(R.id.text_question).text = view.resources.getString(R.string.end_test, state)
//            view.findViewById<TextView>(R.id.text_question).text =   // "Your state is " + state + ". Sending to server..."
            view.findViewById<Button>(R.id.button_ans_1).visibility = View.GONE
            view.findViewById<Button>(R.id.button_ans_2).visibility = View.GONE
            view.findViewById<Button>(R.id.button_ans_3).visibility = View.GONE
            checkResult(view)

        }
    }


    fun checkResult(view: View){
        // request certificate from server with result
        val key = view.resources.getString(R.string.CommandKey)
        val username = view.resources.getString(R.string.CommandName)

        val client = OkHttpClient()
        val request = Request.Builder()
            .url("http://10.0.2.2/check/$key/$username/$state")
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Log.d(TAG, "onFailure")
                Log.d(TAG, e.toString())
                //toast error
                activity?.runOnUiThread {
                    Toast.makeText(activity, "Error: " + e.message, Toast.LENGTH_LONG).show()
                }


            }

            override fun onResponse(call: Call, response: Response) {
                Log.d(TAG, "onResponse")
                //response is the picture in base64, so we need to save it to file

                //check response type (must be json)
                try {
                    if (response.body?.contentType()?.subtype == "json") {
                        val json = response.body!!.string()
                        val based_picture = json.substringAfter("picture\":\"").substringBefore("\",")
                        Log.d(TAG, json)
                        //save picture to data directory
                        val file = File(activity?.getExternalFilesDir(Environment.DIRECTORY_PICTURES), "certificate.png")
//                        val file = File(file_dir, "certificate.png")

                        file.writeBytes(android.util.Base64.decode(based_picture, android.util.Base64.DEFAULT))
                        //toast success
                        activity?.runOnUiThread {
                            Toast.makeText(activity, view.resources.getString(R.string.end_test_success, file.absolutePath), Toast.LENGTH_LONG).show()
                        }

                        // open certificate and avoid FileUriExposedException
                        val intent = Intent(Intent.ACTION_VIEW)
                        intent.addCategory(Intent.CATEGORY_DEFAULT)
                        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                        intent.setDataAndType(FileProvider.getUriForFile(requireActivity(), requireActivity().getPackageName() + ".provider", file), "image/png")
                        intent.putExtra("mimeType", "image/*")
                        startActivity(Intent.createChooser(intent, "Open File"))





                    }
                    else{
                        //toast error
                        activity?.runOnUiThread {
                            Toast.makeText(activity, view.resources.getString(R.string.end_test_error), Toast.LENGTH_LONG).show()
                        }
                        Log.d(TAG, "Error: response is not json")
                    }
                }
                catch (e: Exception){
                    //toast error
                    activity?.runOnUiThread {
                        Toast.makeText(activity, view.resources.getString(R.string.end_test_error), Toast.LENGTH_LONG).show()
                    }
                    // log error
                    Log.d(TAG, e.toString())

                }


            }
        })
    }


    companion object {
        /**
         * Use this factory method to create a new instance of
         * this fragment using the provided parameters.
         *
         * @param param1 Parameter 1.
         * @param param2 Parameter 2.
         * @return A new instance of fragment QuestionFragment.
         */
        // TODO: Rename and change types and number of parameters
        private const val TAG = "QuestionFragment"
        private var state = "";
        private var qNum = 0;


        @JvmStatic
        fun newInstance(param1: String, param2: String) =
            QuestionFragment().apply {
                arguments = Bundle().apply {
                    putString(ARG_PARAM1, param1)
                    putString(ARG_PARAM2, param2)
                }
            }
    }
}