@app.route("/generate-b64", methods=["POST"])
def generate_b64():
    try:
        import base64
        from io import BytesIO

        if request.content_type and "application/json" in request.content_type:
            data = request.json
        else:
            data = request.form.to_dict()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        filename = f"ITI_Report_{data.get('full_name', 'Participant').replace(' ', '_')}.pdf"
        filepath = f"/tmp/{uuid.uuid4().hex}.pdf"

        generate_pdf(data, filepath)

        with open(filepath, "rb") as f:
            pdf_bytes = f.read()
        os.remove(filepath)

        b64 = base64.b64encode(pdf_bytes).decode("utf-8")

        return jsonify({
            "success": True,
            "base64_pdf": b64,
            "filename": filename,
            "mime_type": "application/pdf"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
