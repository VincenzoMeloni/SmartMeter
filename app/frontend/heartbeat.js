(function() {

    class ECGPulse {
      constructor() {
        this.demo = document.getElementById('demo');
        this.ctx = this.demo.getContext('2d');
        this.w = this.demo.getBoundingClientRect().width;
        this.h = this.demo.getBoundingClientRect().height;

        this.px = 0;
        this.opx = 0;
        this.py = this.h / 2;
        this.opy = this.py;

        this.speed = 0.5;
        this.scanBarWidth = 20;
        this.frame = null;

        this.demo.width = this.w;
        this.demo.height = this.h;

        this.ctx.strokeStyle = '#a60f0f';
        this.ctx.lineWidth = 2.0;
        this.ctx.shadowColor = 'rgba(0,255,0,0.9)';
        this.ctx.shadowBlur = 15;

        this.loop = () => {
          this.px += this.speed;

          this.ctx.clearRect(this.px, 0, this.scanBarWidth, this.h);

          this.ctx.beginPath();
          this.ctx.moveTo(this.opx, this.opy);
          this.ctx.lineTo(this.px, this.py);
          this.ctx.stroke();

          this.opx = this.px;
          this.opy = this.py;

          if (this.opx > this.w) {
            this.px = this.opx = -this.speed;
          }

          this.frame = requestAnimationFrame(this.loop);
        };

        this.frame = requestAnimationFrame(this.loop);
      }
    }

    var ecg = new ECGPulse();

    setInterval(async () => {
      try {
        const res = await fetch("/ecg", { cache: "no-store" });
        const data = await res.json();

        const maxKw = 6;

        let norm = data.value / maxKw;
        norm = Math.max(0, Math.min(1, norm));

        ecg.py = (ecg.h / 2) - (norm - 0.5) * 160;

      } catch (err) {
        console.error("Errore GET ECG:", err);
      }
    }, 120);

}());