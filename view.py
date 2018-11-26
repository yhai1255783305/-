from django.shortcuts import render, redirect
def ali():
    # 商户app_id
    app_id = "2016092100566343"

    notify_url = "http://127.0.0.1:8000/page2/"


    return_url = "http://127.0.0.1:8000/page2/"
    # 商户私钥路径
    merchant_private_key_path = "apps/users/keys/pri.txt"
    alipay_public_key_path = "apps/users/keys/zhi_fu_bao_gong_yao.txt"

    ali_pay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=merchant_private_key_path,
        alipay_public_key_path=alipay_public_key_path,
        debug=True,  # 默认False,
    )
    return ali_pay


def zhifu(request):
    if request.method == "GET":
        return render(request, 'zhifu.html')
    else:
        money = float(request.POST.get('money'))
        ali_pay = ali()
        # 生成支付的url
        query_params = ali_pay.direct_pay(
            subject="充值",
            out_trade_no="x2" + str(time.time()),
            total_amount=money,
        )

        pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)

        return redirect(pay_url)


def page2(request):
    ali_pay = ali()
    if request.method == "POST":
        from urllib.parse import parse_qs



        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]


        print(post_dict)

        sign = post_dict.pop('sign', None)

        status = ali_pay.verify(post_dict, sign)
        if status:
            print(post_dict['stade_status'])
            print(post_dict['out_trade_no'])

        return HttpResponse('POST返回')
    else:
        # QueryDict = {'k':[1],'k1':[11,22,3]}
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = ali_pay.verify(params, sign)
        print('GET验证', status)
        return render(request,'index.html')
